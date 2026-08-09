import { memo } from "react";
import { ResultIcon } from "../Shared/Icon";

export const Footer = memo(function Footer() {
  return (
    <footer className="rv2-footer">
      <ResultIcon name="footer" />
    </footer>
  );
});
