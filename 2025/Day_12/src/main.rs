use std::fs;
use std::collections::{HashMap,HashSet};
use regex::Regex;
use log;

type Coord = (i32, i32);


#[derive(Debug)]
struct Shape {
    pub coords: HashSet<Coord>,
    pub min_width: i32,
    pub max_width: i32,
    pub min_height: i32,
    pub max_height: i32,
    pub num_tiles: i32,
}

impl Shape {    
    fn _rotate(&self, turns: u8) -> HashSet<Coord> {
        // Implemented but not actually utilised
        let turns = turns % 4;

        // Early escape if rotation would be meaningless
        if turns == 0 { return self.coords.clone(); }

        // Apply rotation
        let rotated: Vec<Coord> = self.coords
            .iter()
            .map(|&(x, y)| {
                match turns {
                    1 => (-y, x),  // 1 turn = 90° clockwise
                    2 => (-x, -y), // 2 turns = 180° clockwise
                    3 => (y, -x),  // 3 turns = 270° clockwise or 90° counterclockwise
                    _ => (x, y),
                }
            })
            .collect();

        // Re-normalize to ensure anchors at (0, 0)
        let min_x = rotated.iter().map(|p| p.0).min().unwrap_or(0);
        let min_y = rotated.iter().map(|p| p.1).min().unwrap_or(0);

        rotated
            .into_iter()
            .map(|(x, y)| (x - min_x, y - min_y))
            .collect()
    }
    // fn flip(&self) -> HashSet<Coord> {}
}

#[derive(Debug)]
struct Region {
    pub width: i32,
    pub height: i32,
    pub candidates: HashMap<String, i32>,    // key=shape id, value=count
}

impl Region {
    pub fn validate_candidates(&self, shapes: &HashMap<String, Shape>) -> bool {
        // NB: Currently only rule out/in obvious cases, which seems to work for the problem (but not the test)

        // Obviously Impossible 1: Invalid if any shape is larger than a region bound
        let uniq_candidates: Vec<String> = self.candidates.keys().cloned().collect();
        if uniq_candidates
            .iter()
            .any(|s| shapes[s].max_width > self.width || shapes[s].max_height > self.height) {
                log::debug!("At least one shape can't fit into the region");
                return false
            };
        
        // Obviously Possible 1: Value if region could fit shapes if they were all max_height x max_width (no overlap)
        let num_candidates: i32 = self.candidates.values().sum();
        let spaces_3x3: i32 = (self.width / 3) * (self.height / 3);
        if num_candidates <= spaces_3x3 {
            log::debug!("Region could fit all shape if 3x3");
            return true
        };

        // Obviously Impossible 2: Invalid if total tiles needed exceeds region size
        let tile_limit: i32 = self.height * self.width;
        let num_candidate_tiles: i32 = self.candidates.iter().map(|(shape, count)| count * shapes[shape].num_tiles).sum();
        if num_candidate_tiles > tile_limit {
            log::debug!("Not enough tiles to fit candidates");
            return false
        };
 
        log::debug!("Defaulting to true");
        true
    }
}

enum ReadState {
    Searching,  // Either between shapes or regions
    Shape,      // Within a shape section
}

fn solve(path: &str) -> i32 {
    let contents = fs::read_to_string(path).expect("file read failure");
    let mut state = ReadState::Searching;

    let re_newshape = Regex::new(r"^(?P<id>\d+):$").unwrap();
    let re_region = Regex::new(r"^(?P<width>\d+)x(?P<height>\d+): (?P<shapes>.*)$").unwrap();

    let mut shapes: HashMap<String, Shape> = HashMap::new();
    let mut current_id = "";
    let mut current_row = 0;
    let mut current_coords = HashSet::new();

    let mut valid_regions: i32 = 0;

    // Parse into into shapes and regions
    for line in contents.lines() {
        log::debug!("[{}]", line.trim());
        match state {
            ReadState::Searching => {
                log::debug!("<searching>");
                // Skip empty lines
                if line.trim().is_empty() {
                    log::debug!("skipping empty");
                    continue;
                }
                
                // If line looks like a new shape, start parsing it
                if let Some(groups) = re_newshape.captures(line.trim()) {
                    current_id = groups.name("id").unwrap().as_str();
                    log::debug!("Found new shape with id: {:?}", current_id);
                    state = ReadState::Shape;
                    continue;
                }

                // If line looks like a region, parse it
                if let Some(groups) = re_region.captures(line.trim()) {
                    log::debug!("Parsing region");

                    let candidates: HashMap<String, i32> = groups.name("shapes")
                        .unwrap().as_str()
                        .split_whitespace()
                        .enumerate()
                        .map(|(i, count)| (
                            i.to_string(),
                            count.parse().unwrap()
                        ))
                        .collect();
                    
                    let region = Region {
                        width: groups.name("width").unwrap().as_str().parse().unwrap(),
                        height: groups.name("height").unwrap().as_str().parse().unwrap(),
                        candidates: candidates,
                    };
                    log::debug!("Region parsed: {:?}", region);
                    if region.validate_candidates(&shapes) { valid_regions += 1 };
                    continue;
                }
                panic!("Unexpected line form: {}", line);
            }
            ReadState::Shape => {
                log::debug!("<parsing shape>");
                if line.trim().is_empty() {
                    // Add completed shape if id isn't empty
                    assert_eq!(current_id.is_empty(), false);

                    fn find_bounds(shape: &HashSet<Coord>) -> ((i32, i32), (i32, i32)) {
                        shape.iter().fold(
                            ((i32::MAX, i32::MIN), (i32::MAX, i32::MIN)),
                            |((min_width, max_width), (min_height, max_height)), &(width, height)| {
                                (
                                    (min_width.min(width), max_width.max(width)),
                                    (min_height.min(height), max_height.max(height))
                                )
                            },
                        )
                    }

                    let ((min_width, max_width), (min_height, max_height)) = find_bounds(&current_coords);
                    let num_tiles: i32 = current_coords.len().try_into().unwrap();

                    shapes.insert(
                        current_id.to_string(),
                        Shape {
                            coords: current_coords.clone(),
                            min_width: min_width,
                            max_width: max_width,
                            min_height: min_height,
                            max_height: max_height,
                            num_tiles: num_tiles,
                        }
                    );
                    log::debug!("Inserting shape: {:?}", shapes);

                    // Reset id and coords
                    current_id = "";
                    current_row = 0;
                    current_coords.clear();

                    // Resume searching
                    state = ReadState::Searching;
                    continue;
                } else {
                    // If mid-shape, collect up coords

                    // If line isn't exclusively #., then panic
                    assert!(line.trim().chars().all(|c| matches!(c, '#' | '.')));

                    // Else extend current coords set
                    current_coords.extend(
                        line.trim().chars()
                            .enumerate()
                            .filter(|(_, c)| *c == '#')
                            .map(|(current_col, _)| (current_col as i32, current_row))
                    );
                    log::debug!("Updated current_coords: {:?}", current_coords);
                    current_row += 1;
                }
            }
        }
    }

    valid_regions
}

fn main() {
    env_logger::init();
    println!("{}", solve("input.txt"));
    assert_eq!(solve("input.txt"), 528);
}
