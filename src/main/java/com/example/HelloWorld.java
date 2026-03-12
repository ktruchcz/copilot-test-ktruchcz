package com.example;

/**
 * Entry point for the Hello World application.
 */
public class HelloWorld {

    public static void main(String[] args) {
        Greeter greeter = new Greeter();
        String name = (args.length > 0) ? args[0] : null;
        System.out.println(greeter.greet(name));
    }
}
