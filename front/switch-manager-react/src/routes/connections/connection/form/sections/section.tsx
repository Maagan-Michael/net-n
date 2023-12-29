import clsx from "clsx";

export default function FormSection({
  title,
  ltr,
  rightComponent,
  children,
}: React.PropsWithChildren<{
  title: string;
  ltr: boolean;
  rightComponent?: React.ReactNode;
}>) {
  return (
    <div className="p-2">
      <div className="flex flex-row items-center justify-between">
        <h3
          className={clsx(
            "font-bold text-xl",
            ltr ? "text-left" : "text-right"
          )}
        >
          {title}
        </h3>
        {rightComponent}
      </div>
      <div className="relative flex flex-col gap-y-2">{children}</div>
    </div>
  );
}
