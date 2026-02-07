open System

// Define supported operations
type Operation =
    | Add of float * float
    | Subtract of float * float
    | Multiply of float * float
    | Divide of float * float
    | Power of float * float
    | Sqrt of float
    | Sin of float
    | Cos of float
    | Tan of float

// Pure helper functions
let add x y = x + y
let subtract x y = x - y
let multiply x y = x * y
let divide x y = 
    if y = 0.0 then Error "Division by zero"
    else Ok (x / y)
let power x y = x ** y
let sqrtOp x = 
    if x < 0.0 then Error "Cannot calculate square root of a negative number"
    else Ok (Math.Sqrt x)
let sinOp x = Math.Sin x
let cosOp x = Math.Cos x
let tanOp x = Math.Tan x

// Function to execute the operation
let calculate op =
    match op with
    | Add (x, y) -> Ok (add x y)
    | Subtract (x, y) -> Ok (subtract x y)
    | Multiply (x, y) -> Ok (multiply x y)
    | Divide (x, y) -> divide x y
    | Power (x, y) -> Ok (power x y)
    | Sqrt x -> sqrtOp x
    | Sin x -> Ok (sinOp x)
    | Cos x -> Ok (cosOp x)
    | Tan x -> Ok (tanOp x)

// Helper to read float input safely
let rec readFloat prompt =
    printf "%s" prompt
    match Double.TryParse(Console.ReadLine()) with
    | true, value -> value
    | false, _ -> 
        printfn "Invalid number. Please try again."
        readFloat prompt

// Helper to print result
let printResult result =
    match result with
    | Ok res -> printfn "Result: %f" res
    | Error msg -> printfn "Error: %s" msg

// Higher-order function to handle binary operations
let runBinary opName opConstructor =
    printfn "--- %s ---" opName
    let x = readFloat "Enter first number: "
    let y = readFloat "Enter second number: "
    calculate (opConstructor (x, y)) |> printResult

// Higher-order function to handle unary operations
let runUnary opName prompt opConstructor =
    printfn "--- %s ---" opName
    let x = readFloat prompt
    calculate (opConstructor x) |> printResult

// Main application loop (Recursive)
let rec mainLoop () =
    printfn "\nChoose an operation:"
    printfn "1. Add (+)"
    printfn "2. Subtract (-)"
    printfn "3. Multiply (*)"
    printfn "4. Divide (/)"
    printfn "5. Power (^)"
    printfn "6. Square Root (sqrt)"
    printfn "7. Sine (sin)"
    printfn "8. Cosine (cos)"
    printfn "9. Tangent (tan)"
    printfn "0. Exit"
    printf "Enter choice: "

    match Console.ReadLine() with
    | "1" -> 
        runBinary "Addition" Add
        mainLoop ()
    | "2" -> 
        runBinary "Subtraction" Subtract
        mainLoop ()
    | "3" -> 
        runBinary "Multiplication" Multiply
        mainLoop ()
    | "4" -> 
        runBinary "Division" Divide
        mainLoop ()
    | "5" -> 
        // Power is binary: base and exponent
        printfn "--- Power ---"
        let x = readFloat "Enter base: "
        let y = readFloat "Enter exponent: "
        calculate (Power (x, y)) |> printResult
        mainLoop ()
    | "6" -> 
        runUnary "Square Root" "Enter number: " Sqrt
        mainLoop ()
    | "7" -> 
        runUnary "Sine" "Enter angle (radians): " Sin
        mainLoop ()
    | "8" -> 
        runUnary "Cosine" "Enter angle (radians): " Cos
        mainLoop ()
    | "9" -> 
        runUnary "Tangent" "Enter angle (radians): " Tan
        mainLoop ()
    | "0" -> 
        printfn "Exiting..."
        0 
    | _ -> 
        printfn "Invalid choice, please try again."
        mainLoop ()

[<EntryPoint>]
let main argv =
    printfn "Welcome to the Functional Calculator!"
    mainLoop ()
