import * as React from "react";
import CircularProgress from "@mui/material/CircularProgress";
import { styled } from "@mui/material/styles";
import module from "./Loading.module.scss";

const CircleLoading = styled(CircularProgress)`
  color: #ee0033;
`;
export default function Loading() {
  return (
    <div className={module.wrapLoading}>
      <CircleLoading />
    </div>
  );
}
