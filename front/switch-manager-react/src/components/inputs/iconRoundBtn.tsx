import clsx from "clsx";
export default function IconRoundBtn({
  icon,
  text,
  onClick,
  className,
}: {
  icon?: React.ReactNode;
  onClick?: (e: React.MouseEvent<HTMLElement, MouseEvent>) => void;
  text?: string;
  className?: string;
}) {
  return (
    <button
      className={clsx(
        "rounded-full text-md uppercase font-thin tracking-wide bg-white shadow hover:shadow-md flex items-center justify-center cursor-pointer transition-all",
        className
      )}
      onClick={onClick}
    >
      {icon ? icon : <span>{text}</span>}
    </button>
  );
}
