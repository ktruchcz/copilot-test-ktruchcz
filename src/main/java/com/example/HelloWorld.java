package com.example;

public class HelloWorld {

    public String getGreeting() {
        return "Hello, World!";
    }

    public static void main(String[] args) {
        var app = new HelloWorld();
        System.out.println(app.getGreeting());
    }
}
