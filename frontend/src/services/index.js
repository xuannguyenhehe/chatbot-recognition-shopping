import { all } from "redux-saga/effects";
import MessageSagas from "./message";
import UserSagas from "./user";
import ChatSagas from "./chat";

export default function* rootSaga() {
  yield all([
    MessageSagas(),
    UserSagas(),
    ChatSagas(),
  ]);
}
