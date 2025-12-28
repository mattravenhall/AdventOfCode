use std::fs;
use std::rc::Rc;
use std::collections::HashMap;
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

    pub fn count_paths_to(&self, goal: &str, required_nodes: Option<&[&str]>) -> u64 {
        let required_nodes_cleaned = required_nodes.unwrap_or(&[]);

        // Encode nodes numerically ('tokenise'), this enables our bitmask
        let mut required_map = HashMap::new();
        for (i, &node_name) in required_nodes_cleaned.iter().enumerate() {
            required_map.insert(node_name, i);
        }

        // Create our target_mask, this encodes what a valid path's mask will look like
        // (it'll contain len required nodes)
        let target_mask = (1u32 << required_nodes_cleaned.len()) - 1;

        // Cache search states as (key=(node, mask of required nodes found), value=n counts from node to out)
        let mut memo: HashMap<(String, u32), u64> = HashMap::new();

        // Start counting
        self.dfs_count(goal, 0, target_mask, &required_map, &mut memo)
    }

    fn dfs_count(
        &self,
        goal: &str,
        mut current_mask: u32,
        target_mask: u32,
        required_map: &HashMap<&str, usize>,
        memo: &mut HashMap<(String, u32), u64>,
    ) -> u64 {
        // If current node is required, update the mask
        if let Some(&bit_index) = required_map.get(self.name.as_str()) {
            current_mask |= 1 << bit_index;
        }

        // If we're at the goal, return 1 if the path is valid
        if self.name == goal {
            return if current_mask == target_mask { 1 } else { 0 };
        }

        // If we've been here before, just return the count at this point
        let state = (self.name.clone(), current_mask);
        if let Some(&count) = memo.get(&state) {
            return count;
        }

        // Otherwise, start counting paths in children
        let mut total_paths = 0;
        for child in self.children.borrow().iter() {
            total_paths += child.dfs_count(goal, current_mask, target_mask, required_map, memo);
        }

        // Then update our cache with "(node, current_mask): n_paths_to_goal"
        memo.insert(state, total_paths);
        total_paths
    }
}

// Fixed the Option syntax and changed start to &str for flexibility
fn solve(path: &str, start: &str, via: Option<&[&str]>) -> u64 {
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
                let parent = groups.name("parent").unwrap().as_str().to_string();
                // let parent: String = String::from(groups.name("parent").unwrap().as_str().to_string());
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

    // Count paths from `start` to `out` through optional `via` nodes
    let end = "out";
    nodes.get(start)
        .map(|start_node| start_node.count_paths_to(end, via))
        .unwrap_or(0)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {    
    // Part One: Count paths
    assert_eq!(solve("test.txt", "you", None), 5);
    println!("Part One: {:?}", solve("input.txt", "you", None));

    // Part Two: Count paths with required nodes
    let required = ["dac", "fft"];
    assert_eq!(solve("test2.txt", "svr", Some(&required)), 2);
    println!("Part Two: {:?}", solve("input.txt", "svr", Some(&required)));

    Ok(())
}