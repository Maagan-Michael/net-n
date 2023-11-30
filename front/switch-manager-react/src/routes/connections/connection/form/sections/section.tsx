import clsx from "clsx";

export default function FormSection({
  title,
  ltr,
  children,
}: React.PropsWithChildren<{
  title: string;
  ltr: boolean;
}>) {
  return (
    <div className="p-2 col-span-5">
      <h3
        className={clsx("font-bold text-xl", ltr ? "text-left" : "text-right")}
      >
        {title}
      </h3>
      <div className="flex flex-col gap-y-2">{children}</div>
    </div>
  );
}
