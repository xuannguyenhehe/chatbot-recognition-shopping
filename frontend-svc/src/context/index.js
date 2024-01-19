import { combineReducers } from "redux";
import message from "./message";
import chat from "./chat";
import account from "./account";
import image from "./image";
import qa from "./qa";

export default combineReducers({
    message: message.reducer,
    chat: chat.reducer,
    account: account.reducer,
    image: image.reducer,
    qa: qa.reducer,
});
