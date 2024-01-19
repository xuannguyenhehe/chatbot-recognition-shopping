import { all } from "redux-saga/effects";
import MessageSagas from "./message";
import ChatSagas from "./chat";
import AccountSagas from "./account";
import ImageSagas from "./image";
import QASagas from "./qa";

export default function* rootSaga() {
  yield all([
    MessageSagas(),
    ChatSagas(),
    AccountSagas(),
    ImageSagas(),
    QASagas(),
  ]);
}
