import { useState, useCallback, MouseEventHandler } from "react";
import clsx from "clsx";
import { SearchBar } from "./SearchBar";
import SearchIcon from "@icons/search.svg?react";
import SettingsIcon from "@icons/settings.svg?react";
import Cross from "@icons/cross.svg?react";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

export default function Navigation() {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const { i18n } = useTranslation();
  const onSearch: MouseEventHandler<HTMLButtonElement> = useCallback(
    (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (!open) {
        setOpen(true);
      } else {
        setOpen(false);
      }
    },
    [open]
  );
  return (
    <>
      <nav className="fixed w-full bottom-0 right-0 lg:relative lg:w-auto lg:block items-center gap-x-4 mt-4 md:mt-0 z-10">
        <h1 className="hidden lg:block font-thin text-xl md:text-3xl">
          SwitchManager
        </h1>
        <section
          className={clsx(
            "fixed w-full left-0 transition-all lg:transition-none p-4 pr-16 lg:relative lg:grow lg:w-[440px] lg:px-0 lg:py-2 lg:mt-1",
            open ? "bottom-0" : "-bottom-full"
          )}
        >
          <SearchBar shouldFocus={open} onSearchDone={() => setOpen(false)} />
        </section>
        <section>
          <div className="lg:hidden fixed bottom-3 right-3 w-[48px] h-[98px] rounded-md backdrop-blur-md">
            &nbsp;
          </div>
          <button
            className={clsx(
              "absolute bottom-16 lg:top-0 cursor-pointer hover:text-blue-400 transition-all rounded-full bg-neutral-50 shadow-lg lg:shadow-md hover:shadow-lg flex items-center justify-center w-10 h-10",
              "lg:end-4 right-4 lg:right-[unset]"
            )}
            onClick={() => navigate(`/settings?${window.location.search}`)}
          >
            <SettingsIcon className="h-6" />
          </button>
          <button
            className="lg:hidden w-10 h-10 rounded-full flex items-center justify-center rounded-full bg-neutral-50 absolute right-4 bottom-0 transform -translate-y-1/2 shadow-md"
            onMouseDown={onSearch}
          >
            {open ? <Cross /> : <SearchIcon />}
          </button>
        </section>
      </nav>
    </>
  );
}
