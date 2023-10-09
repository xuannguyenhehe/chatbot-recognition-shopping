import { combineReducers } from "redux";
import message from "./message";
import chat from "./chat";
import user from "./user";
import account from "./account";

export default combineReducers({
    message: message.reducer,
    chat: chat.reducer,
    user: user.reducer,
    account: account.reducer,
});
