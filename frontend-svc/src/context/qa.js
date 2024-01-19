import { createSlice } from "@reduxjs/toolkit";

const QA = createSlice({
    name: "qa",
    initialState: {
        intents: [],
        statusTrain: null,
        isLoading: null,
        isUploadAction: false,
    },
    reducers: {
        getState(state) {
            return state;
        },
        saveState(state, { payload }) {
            return { ...state, ...payload };
        },
        changeIsUploadAction(state) {
            return {...state, isUploadAction: !state.isUploadAction}
        }
    },
});

export default QA;
