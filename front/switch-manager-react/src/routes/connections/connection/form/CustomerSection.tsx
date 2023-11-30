import { UseFormRegister } from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import { useTranslation } from "react-i18next";
import clsx from "clsx";

const CustomerSection = ({ register }: { register: UseFormRegister<any> }) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.customer",
  });
  return (
    <div className="p-4 col-span-5">
      <h3
        className={clsx(
          "font-bold text-2xl",
          i18n.dir() === "ltr" ? "text-left" : "text-right"
        )}
      >
        {t("title")}
      </h3>
      <div className="flex flex-col gap-y-2 mt-4">
        <TextInput
          register={register}
          name="customer.firstname"
          label={t("firstname")}
          required
        />
        <TextInput
          register={register}
          name="customer.lastname"
          label={t("lastname")}
          required
        />
        <TextInput
          register={register}
          name="customer.type"
          label={t("type")}
          required
        />
      </div>
    </div>
  );
};

export default CustomerSection;
