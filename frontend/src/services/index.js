import { all } from "redux-saga/effects";
import MessageSagas from "./message";
import ChatSagas from "./chat";
import AccountSagas from "./account";

export default function* rootSaga() {
  yield all([
    MessageSagas(),
    ChatSagas(),
    AccountSagas(),
  ]);
}
