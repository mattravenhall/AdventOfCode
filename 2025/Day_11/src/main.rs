use std::fs;
use std::rc::Rc;
use std::collections::HashMap;
use std::collections::HashSet;
use regex::Regex;
use std::cell::RefCell;


#[derive(Debug)]
struct Node {
    pub name: String,
    pub children: RefCell<Vec<Rc<Node>>>,
}

impl Node {
    fn new(name: &str) -> Rc<Self> {
        Rc::new(Node {
            name: name.to_string(),
            children: RefCell::new(vec![]),
        })
    }

    fn add_child(&self, child: Rc<Self>) {
        self.children.borrow_mut().push(child);
    }

    fn trace_paths_to<'a>(&'a self, goal: &str, path: Option<Vec<String>>) -> HashSet<Option<Vec<String>>> {
        // println!("considering: {}", self.name);
        // Either continue or create a new path
        let mut path = path.unwrap_or(Vec::new());
        let mut completed_paths = HashSet::new();

        path.push(self.name.to_string());
        //println!("current path: {:#?}", path);

        // If we're at the goal, return the path
        if self.name == goal {
            // println!("name {} matches goal {}", self.name, goal);
            //println!("name {} matches goal {} - path: {:#?}", self.name, goal, path);
            if path.len() > 0 {
                // println!("path is len {}, added to completed_paths", path.len());
                completed_paths.insert(Some(path));
            }
            // println!("returning completed_paths"); //: {:#?}", completed_paths);
            return completed_paths;
        }

        // Continue traversing children, if they exist
        if self.children.borrow().len() != 0 {
            // println!("children exist");
            // Otherwise continue searching for paths
            for child in self.children.borrow().iter() {
                let found_paths = child.trace_paths_to(goal, Some(path.clone()));
                if found_paths.len() > 0 {
                    // println!("found a path");
                    completed_paths.extend(found_paths);
                }
            }
        }
        return completed_paths;
    }
}


fn solve_one(path: &str) -> usize {
    let contents = fs::read_to_string(path).unwrap();
    let mut nodes: HashMap<String, Rc<Node>> = HashMap::new();

    let re_edges = Regex::new(r"^(?P<parent>\w+): (?P<children>.*)$").unwrap();

    // Build DAG
    for line in contents.lines() {
        if line.trim().is_empty() {
            continue;
        }
        match re_edges.captures(&line) {
            Some(groups) => {
                let parent: String = String::from(groups.name("parent").unwrap().as_str().to_string());
                let children = groups.name("children").unwrap().as_str().split_whitespace();
                
                let parent_node = nodes.entry(parent.to_string())
                    .or_insert_with(|| Node::new(&parent))
                    .clone();
                
                for child in children {
                    let child_node = nodes.entry(child.to_string())
                        .or_insert_with(|| Node::new(child))
                        .clone();
                    parent_node.add_child(Rc::clone(&child_node));
                }
            }
            None => {
                eprintln!("Warning: Unexpected line {}", line);
            }
        }
    }

    // Count paths from you to out
    let start = String::from("you");
    let end = String::from("out");
    let paths = nodes.get(&start).unwrap().trace_paths_to(&end, None);
    // println!("{:#?}", paths);
    paths.len()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    assert_eq!(solve_one("test.txt"), 5);
    println!("{}", solve_one("input.txt"));
    Ok(())
}
