mod solve;

use clap::Parser;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    day: u8,

    #[arg(short, long, action)]
    test: bool,
}

fn main() {
    let args = Args::parse();

    solve::for_day(args.day, args.test);
}
