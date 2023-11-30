import { UseFormRegister } from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import { useTranslation } from "react-i18next";
import FormSection from "./section";

const CustomerSection = ({ register }: { register: UseFormRegister<any> }) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.customer",
  });
  return (
    <FormSection title={t("title")} ltr={i18n.dir() === "ltr"}>
      <div className="flex flex-row gap-x-2">
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
      </div>
      <TextInput
        register={register}
        name="customer.type"
        label={t("type")}
        required
      />
    </FormSection>
  );
};

export default CustomerSection;
