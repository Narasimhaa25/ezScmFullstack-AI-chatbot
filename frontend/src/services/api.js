import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

export const loginUser = async (email, password) => {
  const res = await API.post("/auth/login", { email, password });
  return res.data;
};

export const signupUser = async (username, email, password) => {
  const res = await API.post("/auth/signup", { username, email, password });
  return res.data;
};