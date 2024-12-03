mod day_01;
mod day_02;
mod day_03;

pub fn for_day(day: u8, test: bool) {
    let path: String = if test { format!("../Day_{:0>2}/test.txt", day) } else { format!("../Day_{:0>2}/input.txt", day) };
    println!("Input Path: {}", path);

    match day {
        1 => day_01::solve(path),
        2 => day_02::solve(path),
        3 => day_03::solve(path),
        _ => { println!("Day {} not recognised", day); },
    }
}
