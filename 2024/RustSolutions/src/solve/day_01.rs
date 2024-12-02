use std::collections::HashMap;
use std::fs;
use regex::Regex;

pub fn solve(input_path: String) {
    let contents = fs::read_to_string(input_path).expect("Can't read file");

    let re_values = Regex::new(r"\d+").unwrap();

    let mut values_left: Vec<u32> = Vec::new();
    let mut values_right: Vec<u32> = Vec::new();
    let mut counts_right = HashMap::new();

    // Collect values into two vectors for part A, plus a hashmap for part B
    for line in contents.split('\n') {
        let matches: Vec<u32> = re_values.find_iter(line).map(|value| value.as_str().parse::<u32>().unwrap()).collect();
        if matches.len() == 2 {
            values_left.push(matches[0]);
            values_right.push(matches[1]);

            let count_key: String = format!("{}", matches[1]); //.to_string();
            match counts_right.get(&count_key) {
                Some(count) => { counts_right.insert(count_key, count + 1); }
                None => {counts_right.insert(count_key, 1); }
            }
        }
    }

    // Sort, primarily for part A
    values_left.sort();
    values_right.sort();

    // Calculate solutions A and B
    let mut solutions = HashMap::new();
    solutions.insert("A", 0);
    solutions.insert("B", 0);

    for value in 0..values_left.len() {
        // Update part A solution
        if let Some(current_total) = solutions.get(&"A") {
            let difference = values_left[value].abs_diff(values_right[value]);
            solutions.insert(&"A", current_total + difference);
        }

        // Update part B solution
        if let Some(current_total) = solutions.get(&"B") {
            if let Some(count_right) = counts_right.get(&values_left[value].to_string()) {
                let blah = values_left[value] * count_right;
                solutions.insert(&"B", current_total + blah);
            }
        }
    }

    // Report solutions
    println!("Solution (Part A): {}", solutions.get(&"A").unwrap());
    println!("Solution (Part B): {}", solutions.get(&"B").unwrap())

}
