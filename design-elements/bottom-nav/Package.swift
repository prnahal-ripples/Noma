// swift-tools-version: 6.0
import PackageDescription

// NOMA bottom navigation — minimizable floating tab bar.
//
// macOS is listed ONLY so the sources can be typechecked on a machine with
// Command Line Tools and no iOS SDK (`swift build`). iOS is the real target;
// nothing here is designed to ship on macOS.
//
// `Demo/` is excluded on purpose — it carries the `@main` App entry point,
// which cannot live inside a library target. Drop it into an Xcode app
// target instead. `NomaBottomNavDemo` (the View) IS in the library, so it
// typechecks here and works in Xcode Previews.
let package = Package(
    name: "NomaBottomNav",
    platforms: [.iOS(.v18), .macOS(.v15)],
    products: [
        .library(name: "NomaBottomNav", targets: ["NomaBottomNav"]),
    ],
    targets: [
        .target(
            name: "NomaBottomNav",
            path: "Sources/NomaBottomNav"
        ),
    ]
)
