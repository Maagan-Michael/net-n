import clsx from "clsx";

export interface IconRoundBtnProps
  extends React.HTMLAttributes<HTMLButtonElement> {
  icon?: React.ReactNode;
  text?: string;
  className?: string;
}

export default function IconRoundBtn({
  icon,
  text,
  onClick,
  className,
  ...props
}: IconRoundBtnProps) {
  return (
    <button
      className={clsx(
        "rounded-full text-md uppercase font-thin tracking-wide bg-white shadow hover:shadow-md active:enabled:shadow-inner flex items-center justify-center cursor-pointer transition-all",
        className
      )}
      onClick={onClick}
      {...props}
    >
      {icon ? icon : <span>{text}</span>}
    </button>
  );
}
