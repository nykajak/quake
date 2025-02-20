import { ref } from "vue";
import { api } from "@/api";

export async function checkUser(){
    let res = await api.get("/");
    return res.data.role == "user"
}