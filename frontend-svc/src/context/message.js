import { createSlice } from "@reduxjs/toolkit";

const Message = createSlice({
  name: "message",
  initialState: {
    messages: null,
    currentMessage: "",
    currentImage: null,
    isLoading: null,
    isShowLoading: null,
    isShowImageUploadArea: false,
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
