import React, { useState } from "react";
import "./Register.css";
import Header from "../Header/Header";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const gohome = () => {
    window.location.href = window.location.origin;
  };

  const register = async (e) => {
    e.preventDefault();

    let register_url = window.location.origin + "/djangoapp/register";

    const res = await fetch(register_url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userName: userName,
        password: password,
        firstName: firstName,
        lastName: lastName,
        email: email,
      }),
    });

    const json = await res.json();
    if (json.status) {
      sessionStorage.setItem("username", json.userName);
      window.location.href = window.location.origin;
    } else if (json.error === "Already Registered") {
      alert("The user with same username is already registered");
      window.location.href = window.location.origin;
    } else {
      alert("Registration failed. Please check your details.");
    }
  };

  return (
    <div className="register_container">
      <Header />
      <div className="modalContainer">
        <form className="register_panel" onSubmit={register}>
          <div className="header_title">
            <h2>Sign Up</h2>
          </div>
          <div className="inputs">
            <div className="input">
              <span className="input_field">Username </span>
              <input
                type="text"
                name="username"
                placeholder="Username"
                className="input_field"
                required
                onChange={(e) => setUserName(e.target.value)}
              />
            </div>
            <div className="input">
              <span className="input_field">First Name </span>
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                className="input_field"
                required
                onChange={(e) => setFirstName(e.target.value)}
              />
            </div>
            <div className="input">
              <span className="input_field">Last Name </span>
              <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                className="input_field"
                required
                onChange={(e) => setLastName(e.target.value)}
              />
            </div>
            <div className="input">
              <span className="input_field">Email </span>
              <input
                type="email"
                name="email"
                placeholder="Email Address"
                className="input_field"
                required
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="input">
              <span className="input_field">Password </span>
              <input
                name="psw"
                type="password"
                placeholder="Password"
                className="input_field"
                required
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          <div className="submit_panel">
            <input className="action_button" type="submit" value="Register" />
            <input className="action_button" type="button" value="Cancel" onClick={gohome} />
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
