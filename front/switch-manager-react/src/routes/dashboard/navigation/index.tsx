import { useState, useCallback, MouseEventHandler } from "react";
import clsx from "clsx";
import { SearchBar } from "./SearchBar";
import SearchIcon from "@icons/search.svg?react";
import Cross from "@icons/cross.svg?react";

export default function Navigation() {
  const [open, setOpen] = useState(false);
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
      <nav className="fixed w-full bottom-0 right-0 lg:relative lg:w-auto lg:block items-center gap-x-4 mt-4 md:mt-0">
        <h1 className="hidden lg:block font-thin text-xl md:text-3xl">
          SwitchManager
        </h1>
        <section
          className={clsx(
            "fixed w-full left-0 transition-all p-4 pr-16 lg:relative lg:grow lg:w-[440px] lg:mt-4",
            open ? "bottom-0" : "-bottom-full"
          )}
        >
          <SearchBar shouldFocus={open} onSearchDone={() => setOpen(false)} />
        </section>
        <section>
          <button
            className="lg:hidden w-10 h-10 rounded-full flex items-center justify-center rounded-full bg-white absolute right-4 bottom-0 transform -translate-y-1/2 shadow-md"
            onMouseDown={onSearch}
          >
            {open ? <Cross /> : <SearchIcon />}
          </button>
        </section>
      </nav>
    </>
  );
}
