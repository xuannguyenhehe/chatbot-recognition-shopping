import { createSlice } from "@reduxjs/toolkit";

const Account = createSlice({
  name: "account",
  initialState: {
    idUser: "",
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    role: "",
    users: "",
    responseMessage: "",
    statusCode: "",
    isLoading: null,
  },
  reducers: {
    getState(state) {
      return state;
    },
    saveState(state, { payload }) {
      return { ...state, ...payload };
    },
    handleLogin: (state) => {
      return {
        ...state,
        isLoading: true,
      };
    },
    handleLoginSuccess: (state) => {
      return {
        ...state,
        isLoading: false,
      };
    },
    handleLoginFailure: (state) => {
      return {
        ...state,
        isLoading: false,
      };
    },
  },
});

export default Account;
