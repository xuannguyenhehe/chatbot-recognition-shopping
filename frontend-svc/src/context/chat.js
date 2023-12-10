import { createSlice } from "@reduxjs/toolkit";

const Chat = createSlice({
  name: "chat",
  initialState: {
    chats: [],
    contacts: [],
    searchUsers: [],
    isLoading: null,
  },
  reducers: {
    getState(state) {
      return state;
    },
    saveState(state, { payload }) {
      return {...state, ...payload}
    },
  },
});

export default Chat;
