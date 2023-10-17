import { createSlice } from "@reduxjs/toolkit";

const Message = createSlice({
  name: "message",
  initialState: {
    messages: null,
    isLoading: null,
    isShowLoading: null,
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

export default Message;
