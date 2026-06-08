// configure env
require("dotenv").config()

// import packages
const express = require("express");
const { createServer } = require("http");
const cookieParser = require("cookie-parser");
const path = require("path");
const cors = require("cors");

// import client and port from env
const client_port = process.env.CLIENT_PORT
const port = process.env.PORT

// import routers

// import socket initialiser function

// create app with cors(origin, methods, credentials)
const app = express();
app.use(cors({
    origin : client_port,
    methods : ["GET", "POST", "DELETE", "PUT"],
    credentials : true
}))

// middlewares
app.use(express.json());
app.use(express.urlencoded({ extended:true }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, "public")));

// use routers
app.get("/", (req, res)=>{
    return res.status(200).json({
        message : "working fine"
    })
})

// create HTTP server
const server = createServer(app);

// pass server to socket initialiser function

// start server listen
server.listen(port, ()=>{
    console.log("Server running on port", port)
})