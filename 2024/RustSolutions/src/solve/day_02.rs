use std::collections::HashSet;
use std::fs;

pub fn solve(input_path: String) {
    let contents = fs::read_to_string(input_path).expect("Can't read file");

    let mut safe_reports_a: u32 = 0;
    let mut safe_reports_b: u32 = 0;


   	for line in contents.split('\n') {
   		if line == "" {
   			continue
   		}
   		let levels: Vec<u32> = line.split(' ').map(|value| value.parse::<u32>().unwrap()).collect();

   		if line_is_safe(levels.clone()) {
   			safe_reports_a += 1;
   			safe_reports_b += 1;
   		} else {
   			for index in 0..levels.len() {
   				let levels_wo_i: Vec<u32> = levels.iter().enumerate().filter(|(i, _)| *i != index).map(|(_, x)| *x).collect();
   				if line_is_safe(levels_wo_i) {
   					safe_reports_b += 1;
   					break;
   				}
   			}
   		}
   	}

    // Report solutions
    println!("Solution (Part A): {}", safe_reports_a);
    println!("Solution (Part B): {}", safe_reports_b);
}

fn line_is_safe(levels: Vec<u32>) -> bool {
	let mut direction: Option<bool> = None;
	for i in 0..levels.len()-1 {
		let left = &levels[i];
		let right = &levels[i+1];
		let direction_check: bool = left > right;
		if direction.is_none() {
			direction = Some(direction_check);
		} else {
			if direction != Some(direction_check) {
				return false
			}
		}

		let safe_distances = HashSet::from([1, 2, 3]);
	    if !safe_distances.contains(&left.abs_diff(*right)) {
	    	return false
	    }
    }
    return true
}