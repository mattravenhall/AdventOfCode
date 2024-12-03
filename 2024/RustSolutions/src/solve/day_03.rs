use regex::Regex;
use std::fs;

pub fn solve(input_path: String) {

	let re_part_a = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();
	let re_part_b = Regex::new(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)").unwrap();

	let mut solution_a: u32 = 0;
	let mut solution_b: u32 = 0;

	let mut active: bool = true;

	let contents = fs::read_to_string(input_path).expect("Can't read file");

	for line in contents.split('\n') {
		if line == "" {
   			continue
   		}

   		// Part A
   		let sum_of_muls: u32 = re_part_a.captures_iter(line)
   			.map(|values| {
   				let x: u32 = values[1].parse().expect("Unable to find x value in mul()");
   				let y: u32 = values[2].parse().expect("Unable to find y value in mul()");
   				x * y
   			}).sum();

   		solution_a += sum_of_muls;

   		// Part B
   		for command in re_part_b.captures_iter(line) {
   			match (command.get(0).expect("re_part_b match failed").as_str(), active) {
   				(command_str, active) if command_str.starts_with("mul") => {
   					// solution_b += 
   					if active {
						let x: u32 = command.get(1).expect("Unable to find x value in mul()").as_str().parse().expect("x is not a valid u32");
						let y: u32 = command.get(2).expect("Unable to find y value in mul()").as_str().parse().expect("y is not a valid u32");
						let product: u32 = x * y;
						solution_b += product;
   					}
   				}
   				("do()", false) => active = true,
   				("don't()", true) => active = false,
   				_ => (),
   			}
   		}
	}

    // Report solutions
    println!("Solution (Part A): {}", solution_a);
    println!("Solution (Part B): {}", solution_b);

}
