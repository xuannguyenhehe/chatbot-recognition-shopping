import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import styled from "styled-components";
import ChatLogo from "assets/chat.png";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useDispatch, useSelector } from "react-redux";
import { REALM_TYPES } from "constants/users";


function Register() {
  const [values, setValues] = useState({
    username: "",
    password: "",
    confirmPassword: "",
    role: "",
  });
  const account = useSelector((state) => state.account);
  const { isLoading, username } = account;
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    if (username) {
      navigate("/");
    }
  }, [navigate, username]);

  const toastOptions = {
    position: "bottom-right",
    autoClose: 8000,
    pauseOnHover: true,
    draggable: true,
    theme: "dark",
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (handleValidation()) {
      const { password, username, role } = values;
      dispatch({
        type: "account/handleRegister",
        payload: {
          username: username,
          password: password,
          repassword: password,
          role: role.length ? role : REALM_TYPES.USER,
        },
      });
    }
  };

  const handleValidation = () => {
    const { password, confirmPassword, username } = values;
    if (password !== confirmPassword) {
      toast.error("Passwords don't match", toastOptions);
      return false;
    } else if (username.length < 4) {
      toast.error("Username should have at least 4 characters", toastOptions);
      return false;
    } 
    return true;
  };

  return (
    <>
      <FormContainer>
        <form onSubmit={(event) => handleSubmit(event)}>
          <div className="brand">
            <img src={ChatLogo} alt="logo" />
            <h1>chat</h1>
          </div>
          <input
            type="text"
            placeholder="Username"
            name="username"
            onChange={(e) => setValues({ ...values, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            name="password"
            onChange={(e) => setValues({ ...values, password: e.target.value })}
          />
          <input
            type="password"
            placeholder="Confirm password"
            name="confirmPassword"
            onChange={(e) => setValues({ ...values, confirmPassword: e.target.value })}
          />
          <select name="role">
            <option value={REALM_TYPES.USER} defaultValue>User</option>
            <option value={REALM_TYPES.ADMIN}>Shop</option>
          </select>
          <button type="submit" disable={isLoading?.toString()}>
            Create User
          </button>
          <span>
            Already have an account? <Link to="/login">Login</Link>
          </span>
        </form>
      </FormContainer>
      <ToastContainer />
    </>
  );
}

const FormContainer = styled.div`
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  align-items: center;
  background-color: #131324;
  .brand {
    display: flex;
    align-items: center;
    gap: 1rem;
    justify-content: center;
    img {
      height: 5rem;
    }
    h1 {
      color: white;
      text-transform: uppercase;
    }
  }
  form {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    background-color: #00000076;
    border-radius: 2rem;
    padding: 3rem 5rem;
  }
  input, select {
    background-color: transparent;
    padding: 1rem;
    border: 0.1rem solid #4e0eff;
    border-radius: 0.4rem;
    color: white;
    width: 100%;
    font-size: 1rem;
    &:focus {
      border: 0.1rem solid #997af0;
      outline: none;
    }
  }
  button {
    background-color: #4e0eff;
    color: white;
    padding: 1rem 2rem;
    border: none;
    font-weight: bold;
    cursor: pointer;
    border-radius: 0.4rem;
    font-size: 1rem;
    text-transform: uppercase;
    &:hover {
      background-color: #4e0eff;
    }
  }
  span {
    color: white;
    text-transform: uppercase;
    a {
      color: #4e0eff;
      text-decoration: none;
      font-weight: bold;
    }
  }
`;

export default Register;