extern crate rayon;

// fn fib(n: u64) -> u64 {
//     if n < 3 {
//         1
//     } else {
//         fib(n - 1) + fib(n - 2)
//     }
// }

fn par_fib(n: u64) -> u64 {
    if n < 3 {
        1
    } else {
        let (a, b) = rayon::join(|| par_fib(n - 1), || par_fib(n - 2));
        a + b
    }
}


fn main() {
    println!("{}", par_fib(40));
}
