import {
  UseFormRegister,
  UseFormSetValue,
  UseFormWatch,
} from "react-hook-form";
import TextInput from "@components/inputs/TextInput";
import { useTranslation } from "react-i18next";
import FormSection from "./section";
import TextAction from "@/components/inputs/textAction";
import { useCustomersQuery } from "@/api/queries/getCustomers";
import { useState } from "react";

const CustomerSelector = ({
  setValue,
  locked,
}: {
  setValue: UseFormSetValue<any>;
  locked?: boolean;
}) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.customer",
  });
  const [search, setSearch] = useState<string>("");
  const { data, loading } = useCustomersQuery({ search });
  // todo : add loader cursor & no results
  return (
    <FormSection title={t("title")} ltr={i18n.dir() === "ltr"}>
      <TextInput
        name="customerId"
        label={t("search")}
        onChange={(e) => setSearch(e.target.value)}
        disabled={locked}
      />
      <div className="p-2">
        {!locked &&
          data?.map((customer) => (
            <div
              key={customer.id}
              className="grid grid-cols-12 items-center text-xs gap-x-2 cursor-pointer hover:bg-neutral-100 p-1"
              onClick={() => {
                setValue("customerId", customer.id, {
                  shouldDirty: true,
                });
                setValue("customer", customer, {
                  shouldDirty: true,
                });
                setValue("toggled", true, {
                  shouldDirty: true,
                });
              }}
            >
              <div className="col-span-4">{customer.id}</div>
              <div className="col-span-4">{customer.firstname}</div>
              <div className="col-span-4">{customer.lastname}</div>
            </div>
          ))}
      </div>
    </FormSection>
  );
};

const CustomerSectionForm = ({
  register,
  setValue,
  locked,
}: {
  register: UseFormRegister<any>;
  setValue: UseFormSetValue<any>;
  locked?: boolean;
}) => {
  const { t, i18n } = useTranslation("translation", {
    keyPrefix: "connection.form.customer",
  });
  return (
    <FormSection
      title={t("title")}
      ltr={i18n.dir() === "ltr"}
      rightComponent={
        <TextAction
          type="button"
          text={t("unasign")}
          className="text-sm"
          onClick={() => {
            setValue("customerId", null, { shouldDirty: true });
            setValue("toggled", false, { shouldDirty: true });
          }}
          disabled={locked}
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

const CustomerSection = ({
  register,
  setValue,
  watch,
  locked = false,
}: {
  register: UseFormRegister<any>;
  setValue: UseFormSetValue<any>;
  watch: UseFormWatch<any>;
  locked?: boolean;
}) => {
  const customerId = watch("customerId");
  if (customerId == null) {
    return <CustomerSelector setValue={setValue} locked={locked} />;
  }
  return (
    <CustomerSectionForm
      register={register}
      setValue={setValue}
      locked={locked}
    />
  );
};

export default CustomerSection;
