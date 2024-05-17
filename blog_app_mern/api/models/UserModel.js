import mongoose from "mongoose";
import bcrypt from 'bcrypt';


const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true
    },
    firstname: {
        type: String,
        required: false
    },
    lastname: {
        type: String,
        required: false
    },
    email: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    profile_image: {
        type: String,
        required: false
    },
}, { timestamps: true })

userSchema.pre("save", async function () {
    this.password = await bcrypt.hash(this.password, 12);
  });  



const usermodel = mongoose.model('users', userSchema)

export default { usermodel};
