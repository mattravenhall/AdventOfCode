mod day_01;

pub fn for_day(day: u8) {
    let path: String = format!("../../Day_{:0>2}/input.txt", day);

    match day {
        1 => day_01::solve(path),
        _ => { println!("Day {} not recognised", day); },
    }
}
