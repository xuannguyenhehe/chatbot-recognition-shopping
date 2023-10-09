import { createSlice } from "@reduxjs/toolkit";

const Account = createSlice({
  name: "account",
  initialState: {
    idUser: "",
    belongedGroup: "",
    idBelongedGroup: "",
    username: "",
    firstName: "",
    lastName: "",
    email: "",
    role: "",
    users: "",
    responseMessage: "",
    statusCode: "",
    isLoading: null,
    userClientRoles: [],
    resetPassword: ''
  },
  reducers: {
    getState(state) {
      return state;
    },
    saveState(state, { payload }) {
      if (payload?.belongedGroup) state.belongedGroup = payload?.belongedGroup;
      if (payload?.idBelongedGroup) state.idBelongedGroup = payload?.idBelongedGroup;
      if (payload?.username) state.username = payload?.username;
      if (payload?.firstName) state.firstName = payload?.firstName;
      if (payload?.lastName) state.lastName = payload?.lastName;
      if (payload?.email) state.email = payload?.email;
      if (payload?.role) state.role = payload?.role;
      if (payload?.users) state.users = payload?.users;
      if (payload?.responseMessage) state.responseMessage = payload?.responseMessage;
      if (payload?.statusCode) state.statusCode = payload?.statusCode;
      if (payload?.isLoading !== null) state.isLoading = payload?.isLoading;
      if (payload?.resetPassword) state.resetPassword = payload?.resetPassword;
      if (payload?.userClientRoles !== null)
        state.userClientRoles = payload?.userClientRoles;
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
