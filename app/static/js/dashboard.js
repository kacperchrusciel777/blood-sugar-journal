// Obsługa resetu formularza (przycisk Reset)
document.getElementById('resetBtn').addEventListener('click', () => {
    const url = document.getElementById('resetBtn').dataset.url;
    window.location = url;
});

// Wykres Chart.js
const ctx = document.getElementById('glucoseChart')?.getContext('2d');
if (ctx) {
    const glucoseChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: JSON.parse(document.getElementById('glucoseChart').dataset.labels),
            datasets: [{
                label: 'Glucose over time (mg/dL)',
                data: JSON.parse(document.getElementById('glucoseChart').dataset.values),
                borderColor: 'rgba(74, 144, 226, 0.9)',
                backgroundColor: 'rgba(74, 144, 226, 0.25)',
                fill: true,
                tension: 0.3,
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: 'rgba(74,144,226,1)',
                borderWidth: 3,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    suggestedMin: 60,
                    suggestedMax: 200,
                    title: {
                        display: true,
                        text: 'Glucose (mg/dL)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        font: { weight: 'bold' }
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Eksport PDF przycisk
const exportBtn = document.getElementById('exportPdfBtn');
if (exportBtn) {
    exportBtn.addEventListener('click', async () => {
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('p', 'pt', 'a4');
        let y = 40;
        const marginX = 40;
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();

        pdf.setFontSize(18);
        pdf.text('Glucose Dashboard Report', marginX, y);
        y += 30;

        // Dodaj wykres jako obraz PNG z canvas
        const canvas = document.getElementById('glucoseChart');
        const imgData = canvas.toDataURL('image/png');
        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pageWidth - 2 * marginX;
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

        if (y + pdfHeight > pageHeight - 40) {
            pdf.addPage();
            y = 40;
        }
        pdf.addImage(imgData, 'PNG', marginX, y, pdfWidth, pdfHeight);
        y += pdfHeight + 30;

        // Dodaj statystyki
        const statsEl = document.getElementById('stats');
        pdf.setFontSize(14);
        pdf.text('Statistics:', marginX, y);
        y += 20;
        pdf.setFontSize(12);
        pdf.text(`Average glucose: ${statsEl.dataset.avgGlucose} mg/dL`, marginX, y);
        y += 18;
        pdf.text(`Minimum glucose: ${statsEl.dataset.minGlucose} mg/dL`, marginX, y);
        y += 18;
        pdf.text(`Maximum glucose: ${statsEl.dataset.maxGlucose} mg/dL`, marginX, y);
        y += 30;

        // Dodaj notatki w formacie "Glucose: XX mg/dL — DATA (TAG) (NOTATKA)"
        pdf.setFontSize(14);
        pdf.text('Entries:', marginX, y);
        y += 20;
        pdf.setFontSize(11);

        const entriesData = JSON.parse(document.getElementById('entriesData').textContent);

        for (let i = 0; i < entriesData.length; i++) {
            const e = entriesData[i];
            const formattedDate = e.timestamp;

            let line = `Glucose: ${e.glucose} mg/dL — ${formattedDate}`;
            if (e.tag) line += ` (${e.tag})`;
            if (e.note) line += ` (${e.note})`;

            let lines = pdf.splitTextToSize(line, pageWidth - 2 * marginX);
            if (y + lines.length * 14 > pageHeight - 40) {
                pdf.addPage();
                y = 40;
            }
            pdf.text(lines, marginX, y);
            y += lines.length * 14 + 8;
        }

        pdf.save('glucose_dashboard_report.pdf');
    });
}
