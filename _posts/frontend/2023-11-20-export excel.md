---
layout: post
title: "export excel"
date: 2023-11-20
categories: Frontend
tags:
  - React
---

export excel on web required two packages: [file-saver](https://www.npmjs.com/package/file-saver) and [exceljs](https://www.npmjs.com/package/exceljs)

```js
import { saveAs } from "file-saver";
const Excel = require("exceljs");

<Button
  onClick={async () => {
    const workbook = new Excel.Workbook();
    const worksheet = workbook.addWorksheet("自动驾驶Case");
    worksheet.properties.defaultRowHeight = 30;
    worksheet.columns = [
      {
        header: "标签",
        key: "tags",
        width: 20,
      },
      { header: "时间", key: "time", width: 20 },
      { header: "车号", key: "car", width: 10 },
      { header: "描述", key: "overview", width: 50 },
      { header: "门店", key: "location", width: 20 },
      { header: "严重程度", key: "severity", width: 10 },
    ];
    const header = worksheet.getRow(1);
    header.alignment = { vertical: "middle", horizontal: "center" };
    header.font = { bold: true };
    currentCases.forEach((element) => {
      const newRow = worksheet.addRow({
        tags: element.tags.map((tag) => tag.name).join(","),
        time: element.time,
        car: element.car,
        overview: element.overview,
        location: element.location,
        severity: severityMap[element.severity],
      });
      newRow.alignment = { vertical: "middle", horizontal: "center" };
    });

    // await workbook.xlsx.writeFile("export.xlsx");
    const buffer = await workbook.xlsx.writeBuffer();
    const fileType =
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet";
    const fileExtension = ".xlsx";

    const blob = new Blob([buffer], { type: fileType });

    saveAs(
      blob,
      `export${dayjs().format("YYYY-MM-DD HH:mm:ss")}${fileExtension}`
    );
  }}
>
  <div className="flex items-center">
    <TbTableExport />
    导出
  </div>
</Button>
```
