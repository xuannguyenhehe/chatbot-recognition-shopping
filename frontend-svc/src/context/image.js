import { createSlice } from "@reduxjs/toolkit";

const Image = createSlice({
  name: "image",
  initialState: {
    uploadedImages: [],
    isUploadAction: false,
    isLoading: null,
  },
  reducers: {
    getState(state) {
      return state;
    },
    saveState(state, { payload }) {
      return {...state, ...payload}
    },
    changeIsUploadAction(state) {
      return {...state, isUploadAction: !state.isUploadAction}
    }
  },
});

export default Image;
