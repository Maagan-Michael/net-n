export default function DropDownSection({
  label,
  action,
  children,
}: React.PropsWithChildren<{
  label: string;
  action?: React.ReactNode;
}>) {
  return (
    <div>
      <div className="flex justify-between items-center">
        <label className="text-sm font-thin">{label}</label>
        <div>{action}</div>
      </div>
      <div>{children}</div>
    </div>
  );
}
