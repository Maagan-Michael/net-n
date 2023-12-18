import { useNavigate } from "react-router-dom";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";

export default function Settings() {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "settings",
  });
  const goBack = useCallback(
    (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
      e.preventDefault();
      e.stopPropagation();
      navigate(`/${window.location.search}`);
    },
    [navigate]
  );
  return (
    <div className="fixed top-0 left-0 w-full h-full flex justify-center items-center z-20">
      <div className="w-96 h-96 bg-white rounded-lg shadow-lg p-8 z-10">
        <h1>{t("title")}</h1>
        <h2>{t("instructions")}</h2>
        <ul>
          {i18n.languages.map((lang) => (
            <li key={lang}>{lang}</li>
          ))}
        </ul>
      </div>
      <div
        className="absolute top-0 left-0 w-full h-full backdrop-blur-md flex justify-center items-center cursor-pointer hover:backdrop-blur-sm transition-all"
        onMouseDown={goBack}
      ></div>
    </div>
  );
}
