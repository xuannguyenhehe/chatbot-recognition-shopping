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
    isLoading: null,
    noTabChat: null,
    noTabChatbot: 0,
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
