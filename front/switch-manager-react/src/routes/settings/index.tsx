import { useNavigate } from "react-router-dom";
import { useCallback } from "react";
import { useTranslation } from "react-i18next";
import ISO6391 from "iso-639-1";
import clsx from "clsx";
import CrossIcon from "@icons/cross.svg?react";
import TextAction from "@/components/inputs/textAction";

export default function Settings() {
  const navigate = useNavigate();
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "settings",
  });
  const goBack = useCallback(
    (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
      e.preventDefault();
      e.stopPropagation();
      navigate(`/${window.location.search}`);
    },
    [navigate]
  );
  return (
    <div className="fixed top-0 left-0 w-full h-full flex justify-center items-center z-20">
      <div className="relative w-96 h-96 bg-white rounded-lg shadow-lg px-8 pt-8 pb-4 z-10 flex flex-col">
        <button className="absolute top-4 right-4 w-8 h-8" onClick={goBack}>
          <CrossIcon />
        </button>
        <h1 className="font-bold text-center text-xl">{t("title")}</h1>
        <h2 className="my-4 font-light">{t("instructions")}</h2>
        <ul className="text-xs overflow-scroll shadow-inner grow">
          {i18n.languages.map((lang) => (
            <li
              key={lang}
              className={clsx(
                "p-2",
                lang === i18n.language
                  ? "bg-blue-400 cursor-default"
                  : "cursor-pointer bg-neutral-100 hover:bg-blue-200 hover:underline"
              )}
              onClick={() => i18n.changeLanguage(lang)}
            >
              {ISO6391.getNativeName(lang)}
            </li>
          ))}
        </ul>
        <div className="py-2 w-full text-center">
          <TextAction
            onMouseDown={goBack}
            className="font-light text-md"
            text={clsx(t("continue"), " ", i18n.dir() === "rtl" ? "←" : "→")}
          />
        </div>
      </div>
      <button
        className="absolute top-0 left-0 w-full h-full backdrop-blur-md flex justify-center items-center cursor-pointer hover:backdrop-blur-sm transition-all"
        onMouseDown={goBack}
      ></button>
    </div>
  );
}
