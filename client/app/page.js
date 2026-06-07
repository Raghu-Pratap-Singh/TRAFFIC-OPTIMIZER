'use client'
import React, { useState } from "react"

function Page() {
  let [string, SetString] = useState("");
  async function send() {
    let response = await fetch("http://127.0.0.1:8000/", {
      method:"GET",
      credentials:"include"
    })
    let data = await response.json();
    console.log(data)
    SetString(data.message)
  }
  return <>
    <button onClick={()=>{
      send()
    }}>sender</button>
    <h1>{string}</h1>
  </>
}
export default Page;