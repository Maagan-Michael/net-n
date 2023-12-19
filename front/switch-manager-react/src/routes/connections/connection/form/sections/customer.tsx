import { UseFormRegister } from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import { useTranslation } from "react-i18next";
import FormSection from "./section";
import TextAction from "@/components/inputs/textAction";

const CustomerSection = ({ register }: { register: UseFormRegister<any> }) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.customer",
  });
  return (
    <FormSection
      title={t("title")}
      ltr={i18n.dir() === "ltr"}
      rightComponent={
        <TextAction
          className="text-xs"
          text={t("clear")}
          onMouseDown={() => console.log("clear")}
        />
      }
    >
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
      <div className="flex flex-row gap-x-2">
        <TextInput
          register={register}
          name="customer.type"
          label={t("type")}
          required
        />
        <TextInput
          className="w-4/12"
          register={register}
          name="customer.id"
          label={t("ID")}
          disabled
        />
      </div>
    </FormSection>
  );
};

export default CustomerSection;
