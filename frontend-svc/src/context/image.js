import { createSlice } from "@reduxjs/toolkit";

const Image = createSlice({
  name: "image",
  initialState: {
    tempImages: [],
    uploadedImages: [],
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

export default Image;
