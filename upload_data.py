import requests
import json

# URL API Anda
url = "http://localhost:8000/v2/helpdesk/knowledge/add"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Data JSON Lengkap (Dari hasil sebelumnya)
data_list = [
  {
    "title": "Standar Pelayanan Publik Pengusulan Alih Tugas Ke Dalam Jabatan Dosen",
    "description": "Layanan usulan alih tugas pegawai negeri sipil non-dosen menjadi dosen atau perpindahan dosen antar instansi.",
    "content_raw": "Persyaratan Pelayanan: 1. Asli surat Permohonan pindah (bermaterai Rp. 10.000); 2. Asli Surat pernyataan persetujuan menerima dari PTS; 3. Asli Surat pernyataan persetujuan melepas dari Unit Kerja; 4. Asli Surat keterangan mata kuliah yang diampu; 5. Asli surat keterangan rasio dosen dan mahasiswa; 6. Asli surat keterangan sehat jasmani dan rohani dari RS tipe C; 7. Asli surat keterangan bebas narkotika; 8. Asli surat pernyataan tidak sedang tugas belajar; 9. Asli surat pernyataan tidak sedang dalam proses perkara pidana; 10. Asli surat keterangan tidak pernah hukuman disiplin berat 2 tahun terakhir; 11. Asli surat pernyataan tidak sedang banding administratif; 12. Asli surat pernyataan tidak sedang ikatan dinas; 13. Fotokopi SK CPNS; 14. Fotokopi SK PNS; 15. Fotokopi SK Pangkat terakhir; 16. Asli analisis jabatan; 17. Asli analisis beban kerja Dosen; 18. Fotokopi ijazah & transkrip S1, S2; 19. Fotokopi SKP 2 tahun terakhir; 20. Asli Keterangan Penyetaraan Ijazah LN; 21. Asli Surat penolakan dari 2 PTN (untuk pindah ke PTS); 22. Asli Surat Keterangan alasan pindah (bermaterai); 23. Asli Surat Keterangan biaya pendidikan (bermaterai); 24. Asli Surat Keterangan Bebas Temuan Inspektorat; 25. Asli Surat Persetujuan Alih Tugas LLDIKTI IX. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Penerbitan SPT Pajak Tahunan",
    "description": "Layanan penerbitan Surat Pemberitahuan (SPT) Pajak Tahunan bagi pegawai.",
    "content_raw": "Persyaratan Pelayanan: Surat Permohonan yang memuat keterangan terkait Nama dan NIP/NIDN. Prosedur: Pemohon mengajukan melalui SIPINTER, memasukkan OTP email, mengisi form, verifikasi JFU, validasi Ketua Tim Keuangan, dan pemohon menerima dokumen elektronik atau fisik. Jangka Waktu: 3 hari kerja. Biaya: Gratis.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Permintaan Perincian Gaji",
    "description": "Layanan permintaan dokumen rincian gaji pegawai.",
    "content_raw": "Persyaratan Pelayanan: Surat Permohonan yang memuat keterangan terkait NIP, Nama, Nomor Urut Gaji. Prosedur: Pengajuan via SIPINTER, input OTP, upload persyaratan, verifikasi JFU, penandatanganan oleh PPABP, dokumen dikirim atau diambil di ULT. Jangka Waktu: 1 hari kerja. Biaya: Gratis.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Usulan Pembayaran Tunjangan Serdos Selesai Tubel",
    "description": "Layanan pengaktifan kembali pembayaran tunjangan sertifikasi dosen setelah selesai tugas belajar.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Pembayaran Dari Pimpinan PTS; 2. SK Pengaktifan Kembali LLDIKTI IX; 3. Sertifikat Pendidik; 4. BKD/LKD Semester Sebelumnya Memenuhi Syarat; 5. SK Inpassing s.d SK Golongan Terakhir Asli (DTY); 6. SK Golongan Dan KGB Terakhir Asli (DPK); 7. SK Jabatan Fungsional Dan PAK Terakhir; 8. SPTJM Penerima Tunjangan Profesi Asli Bermaterai; 9. Surat Pernyataan Keaslian Dokumen Asli Bermaterai; 10. Rekening BRI Baru, NPWP. Jangka Waktu: 7-15 Hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Pengesahan SK Ijin PTS",
    "description": "Layanan legalisir atau pengesahan Salinan Keputusan Izin Perguruan Tinggi Swasta.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Pengesahan/Legalisir SK Ijin ditujukan Kepala LLDIKTI (oleh Badan Penyelenggara untuk PTS, oleh PT untuk Prodi); 2. Surat Permohonan ditujukan kepada Menteri/Dirjen; 3. Surat Keterangan Kehilangan Kepolisian (jika hilang); 4. Scan SK Ijin Penyelenggaraan; 5. Screenshot Nama PT di PDDIKTI. Jangka Waktu: 10 hari kerja. Biaya: Gratis.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Perubahan Nama Program Studi (Nomenklatur) PTS dan PTN",
    "description": "Layanan rekomendasi perubahan nama program studi bagi PTS dan PTN.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. Screenshot Akun SIAGA/Silemkerma; 4. SK Menkumham Badan Penyelenggara; 5. Pakta Integritas Pimpinan PT; 6. SK Pembukaan Prodi lama; 7. Akta Notaris; 8. Capaian Pembelajaran & Struktur Kurikulum; 9. SK Pendirian PTS; 10. SK Ijin Awal Prodi; 11. SK Perubahan Badan Penyelenggara; 12. Rekomendasi Senat PT. Jangka Waktu: 7 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Prodi PJJ / PSDKU / Alih Jenjang / Kelas Pengembangan",
    "description": "Layanan rekomendasi pembukaan program studi PJJ, PSDKU, atau kelas pengembangan.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. KTP & SK Ketua Tim; 4. Identitas & Pakta Integritas Pengusul; 5. SK Izin Pendirian PT; 6. Sertifikat Akreditasi Prodi; 7. Pakta Integritas Pimpinan PT; 8. Persetujuan Badan Penyelenggara; 9. Sarpras (Foto Lokasi, Lahan, Bangunan); 10. Rekomendasi Senat; 11. Foto Bersama Tim; 12. Screenshot Akun SIAGA/Silemkerma; 13. Rekomendasi Pemda setempat; 14. SK Ijin Prodi. Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Penambahan Prodi Baru PTN",
    "description": "Layanan rekomendasi penambahan program studi baru untuk Perguruan Tinggi Negeri.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. KTP & SK Ketua Tim; 4. Screenshot SIAGA/Silemkerma; 5. Pakta Integritas Pimpinan PT; 6. Identitas & Pakta Integritas Pengusul; 7. Rekomendasi Senat PTN; 8. SK Ijin Pendirian PTN; 9. Daftar Calon Dosen (Tabel, Ijazah, Transkrip). Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Penambahan Prodi Baru PTS - Prodi Akademik",
    "description": "Layanan rekomendasi penambahan program studi akademik (S1/S2/S3/Spesialis) untuk PTS.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. SK Menkumham Badan Penyelenggara; 4. Identitas & Pakta Integritas Tim; 5. SK Izin Pendirian PT; 6. Foto Bersama Tim; 7. SK Perubahan Badan Penyelenggara; 8. KTP & SK Ketua Tim; 9. Pakta Integritas Pimpinan PT; 10. Perjanjian Kerjasama DUDI (Opsional); 11. Akta Notaris; 12. Rekomendasi Senat; 13. Persetujuan Badan Penyelenggara; 14. Screenshot SIAGA; 15. Rekomendasi Lama (jika perpanjangan); 16. Daftar Calon Dosen. Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Penambahan Prodi Baru PTS - Prodi Vokasi",
    "description": "Layanan rekomendasi penambahan program studi vokasi (Diploma) untuk PTS.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen Vokasi; 3. Perjanjian Kerjasama DUDI; 4. Rekomendasi Senat; 5. KTP & SK Ketua Tim; 6. Foto Bersama Tim; 7. Akta Notaris; 8. SK Perubahan Badan Penyelenggara; 9. Identitas & Pakta Integritas Pengusul; 10. SK Menkumham; 11. Pakta Integritas Pimpinan PT; 12. SK Izin Pendirian PT; 13. Persetujuan Badan Penyelenggara; 14. Rekomendasi Lama (jika perpanjangan); 15. Screenshot SILEMKERMA; 16. Daftar Calon Dosen. Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Pendaftaran/Perbaikan Nama PT / Prodi Pada PDDIKTI",
    "description": "Layanan perbaikan nomenklatur nama Perguruan Tinggi atau Program Studi pada Pangkalan Data Pendidikan Tinggi.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. SK Izin Pendirian PT; 4. SK Pembukaan Prodi; 5. Persetujuan Badan Penyelenggara; 6. Rekomendasi Senat; 7. Screenshot Nama PT/Prodi di PDDIKTI. Jangka Waktu: 7 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Pendirian PTS Akademik",
    "description": "Layanan rekomendasi pendirian Perguruan Tinggi Swasta baru jenis Akademik.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen Dikti; 3. Kerjasama DUDI; 4. Foto Bersama Tim; 5. Pakta Integritas Yayasan; 6. KTP & SK Ketua Tim; 7. SK Kemenkumham Yayasan; 8. Identitas & Pakta Integritas Pengusul; 9. Akta Notaris; 10. Studi Kelayakan; 11. Lokasi, Denah, Gambar Gedung; 12. Laporan Keuangan Audit (Yayasan >3 thn) atau Internal (<3 thn); 13. Rekening Koran 3 bulan terakhir; 14. Screenshot Akun SIAGA; 15. Daftar Calon Dosen; 16. Rekomendasi Lama (jika perpanjangan). Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Pendirian PTS Vokasi",
    "description": "Layanan rekomendasi pendirian Perguruan Tinggi Swasta baru jenis Vokasi.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Kerjasama DUDI; 3. Foto Bersama Tim; 4. Pakta Integritas Yayasan; 5. KTP & SK Ketua Tim; 6. SK Kemenkumham Yayasan; 7. Surat Permohonan ke Menteri/Dirjen Vokasi; 8. Identitas & Pakta Integritas Pengusul; 9. Akta Notaris; 10. Studi Kelayakan; 11. Lokasi, Denah, Gambar Gedung; 12. Laporan Keuangan Audit/Internal; 13. Rekening Koran 3 bulan; 14. Screenshot SILEMKERMA; 15. Daftar Calon Dosen; 16. Rekomendasi Lama (jika perpanjangan). Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Penggabungan/Penyatuan PTS",
    "description": "Layanan rekomendasi merger atau penyatuan beberapa PTS.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. KTP & SK Ketua Tim; 4. Studi Kelayakan Merger; 5. Pakta Integritas Yayasan; 6. Sertifikat Lahan/Sewa min 10 thn; 7. Screenshot SIAGA/SILEMKERMA; 8. SK Menkumham Badan Penyelenggara; 9. Akta Notaris Penggabungan; 10. Identitas & Pakta Integritas Pengusul; 11. SK Izin Pendirian masing-masing PTS; 12. Akta Notaris Pendirian masing-masing Yayasan; 13. Foto Bersama Tim; 14. Screenshot PTS di PDDIKTI; 15. Laporan Keuangan Audit/Internal; 16. Rekening Koran; 17. Rekomendasi Seluruh Senat PTS. Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Perubahan Nama / Penetapan Badan Penyelenggara",
    "description": "Layanan rekomendasi perubahan nama Yayasan atau Badan Penyelenggara PTS.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Dirjen; 3. SK Izin Pendirian PT; 4. Akta Notaris Pendirian & Perubahan; 5. Akta/Surat Kronologis Perubahan; 6. SK Menkumham Pengesahan BP; 7. Pakta Integritas BP. Jangka Waktu: 10 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Perubahan Nama PTS",
    "description": "Layanan rekomendasi perubahan nama Perguruan Tinggi Swasta.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. SK Menkumham BP; 4. Akta Notaris Pendirian & Perubahan; 5. Identitas & Pakta Integritas Pengusul; 6. SK Perubahan BP (jika ada); 7. Foto Bersama Tim; 8. Rekomendasi Lama (jika perpanjangan); 9. Pakta Integritas Yayasan; 10. Screenshot SIAGA/SILEMKERMA; 11. KTP & SK Ketua Tim; 12. Rekomendasi Senat PT; 13. SK Izin Pendirian PT; 14. Contoh Ijazah PTS. Jangka Waktu: 10 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Pindah Lokasi PTS",
    "description": "Layanan rekomendasi perpindahan lokasi kampus PTS.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. Kerjasama DUDI di lokasi baru; 4. Foto Bersama Tim; 5. Pakta Integritas Yayasan; 6. KTP & SK Ketua Tim; 7. SK Kemenkumham Yayasan; 8. Identitas & Pakta Integritas Pengusul; 9. Akta Notaris; 10. Studi Kelayakan; 11. Lokasi, Denah, Gambar Gedung; 12. Laporan Keuangan; 13. Rekening Koran; 14. Screenshot SILEMKERMA/SIAGA; 15. Daftar Calon Dosen; 16. Rekomendasi Lama. Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Alih Kelola PTS",
    "description": "Layanan rekomendasi alih kelola pembinaan PTS dari satu Badan Penyelenggara ke Badan Penyelenggara lain.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. Screenshot SIAGA/SILEMKERMA; 4. KTP & SK Ketua Tim; 5. Akta Notaris Pendirian BP Pengalih; 6. Studi Kelayakan Alih Kelola; 7. SK Perubahan BP; 8. SK Menkumham BP Pengalih; 9. SK Menkumham BP Penerima; 10. Identitas & Pakta Integritas Pengusul; 11. Akta Notaris Kesepakatan Alih Kelola; 12. Akta Notaris Pendirian BP Penerima; 13. Pakta Integritas Yayasan; 14. Foto Bersama Tim; 15. SK Izin Pendirian PTS; 16. Laporan Keuangan; 17. Rekening Koran; 18. Rekomendasi Lama. Jangka Waktu: 10 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Penutupan Prodi PTN Dan PTS",
    "description": "Layanan rekomendasi penutupan program studi.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. Pakta Integritas Pimpinan PT; 4. Persetujuan Badan Penyelenggara; 5. Akta Notaris; 6. Pertimbangan Senat PT; 7. SK Pembukaan Prodi; 8. Screenshot Data Dosen/Mhs di PDDIKTI; 9. Screenshot SIAGA/SILEMKERMA; 10. SK Menkumham; 11. SK Perubahan BP; 12. SK Izin Pendirian PT; 13. Rekomendasi Senat; 14. Surat Pernyataan Penyelesaian Kewajiban Dosen/Mhs; 15. Rekomendasi Lama. Jangka Waktu: 7 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Kelembagaan: Usul Perubahan Bentuk PTS",
    "description": "Layanan rekomendasi perubahan bentuk PTS (misal: Sekolah Tinggi menjadi Universitas).",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi ke Kepala LLDIKTI; 2. Surat Permohonan ke Menteri/Dirjen; 3. Foto Bersama Tim; 4. SK Perubahan BP; 5. Identitas & Pakta Integritas Pengusul; 6. Akta Notaris BP; 7. KTP & SK Ketua Tim; 8. Screenshot Usulan Prodi di SIAGA; 9. SK Izin Pendirian PTS; 10. Studi Kelayakan Perubahan Bentuk; 11. SK Menkumham; 12. Pakta Integritas Yayasan; 13. Sertifikat Lahan/Sewa; 14. Screenshot SIAGA/SILEMKERMA; 15. Laporan Keuangan Audit; 16. Rekening Koran; 17. Daftar Calon Dosen. Jangka Waktu: 15 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Permohonan Rekomendasi Perubahan Awal Lapor",
    "description": "Layanan rekomendasi untuk mengubah periode awal pelaporan data PDDIKTI.",
    "content_raw": "Persyaratan Pelayanan: 1. Scan Surat Permohonan Pimpinan PT memuat alasan; 2. Scan SK Penyelenggaraan Prodi (jika prodi); 3. Scan SK Pendirian PT (jika PT); 4. Scan Kalender Akademik periode dimaksud. Jangka Waktu: 3 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Rekomendasi Akreditasi (Ubah Nama)",
    "description": "Layanan rekomendasi akreditasi terkait perubahan nama atau akreditasi pertama.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan Rekomendasi (Akreditasi Pertama/TMSP/Re-Akreditasi); 2. Tangkapan Layar laman SAPTO/LAM. Jangka Waktu: 3 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Permohonan Informasi Publik",
    "description": "Layanan permintaan informasi publik kepada PPID.",
    "content_raw": "Persyaratan Pelayanan: 1. Scan KTP (Pribadi) / Akta Perusahaan / Akta Notaris LSM; 2. Surat Permohonan Informasi detil. Jangka Waktu: 14 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Pengajuan Permohonan Rekomendasi Rusunawa",
    "description": "Layanan rekomendasi pembangunan rumah susun sewa mahasiswa.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Permohonan ke Kepala LLDIKTI; 2. Surat pernyataan kesanggupan penyediaan tanah (siap bangun, akses jalan, bebas banjir, ada air/listrik); 3. SPTJM tanah tidak sengketa & asset yayasan; 4. Scan Sertifikat Tanah & Masterplan (min 2.100 m2); 5. Screenshot Profil PT (Aktif, >300 mhs); 6. Akreditasi PT; 7. Surat pernyataan tidak kena sanksi; 8. Surat pernyataan tidak ada masalah internal. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Penetapan Angka Kredit dan Jabatan Fungsional Dosen Asisten Ahli dan Lektor",
    "description": "Layanan penilaian dan penetapan angka kredit untuk jabatan Asisten Ahli dan Lektor.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat pengantar Rektor; 2. Berita Acara PAK PTS; 3. SK Jafung/Inpassing terakhir; 4. KTP; 5. BKD/LKD 2 thn terakhir (Lektor); 6. SKP; 7. Bukti Pendidikan; 8. Bukti Penelitian; 9. Bukti Pengabdian; 10. Bukti Penunjang; 11. SK Gelar Terakhir. Prosedur melalui SIPINTER dan http://jafa.lldikti9.id. Jangka Waktu: 25 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Penetapan Angka Kredit dan Jabatan Fungsional Lektor Kepala dan Professor",
    "description": "Layanan verifikasi usulan jabatan fungsional Lektor Kepala dan Guru Besar sebelum diajukan ke Pusat.",
    "content_raw": "Persyaratan Pelayanan: 1. Pertimbangan Senat; 2. Abstrak Disertasi; 3. SK Pengaktifan Kembali; 4. Pernyataan Keabsahan Karya Ilmiah; 5. Daftar Hadir Senat; 6. Ket. Melaksanakan Penelitian; 7. Serdik; 8. Pangkat Terakhir; 9. SKP 2 thn; 10. SK Tubel; 11. Validasi Karya Ilmiah; 12. Ijazah & Akreditasi; 13. Daftar Penilaian Bidang A-E & Bukti Kinerja; 14. PAK Terakhir; 15. Jabatan Akademik Terakhir. Prosedur melalui laman pak.kemdikbud.go.id/pakdosen. Jangka Waktu: 30 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Pindah Homebase Dosen Tetap Yayasan",
    "description": "Layanan rekomendasi pindah homebase bagi Dosen Tetap Yayasan.",
    "content_raw": "Persyaratan Pelayanan: 1. SK Pemberhentian/Lolos Butuh dari PTS asal; 2. Surat permohonan pindah; 3. SK CPNS (jika lulus PNS); 4. SK Dosen Tetap/Kesediaan Menerima PT Tujuan; 5. Rekomendasi LLDIKTI Asal (Lintas Wilayah); 6. Ijazah Terakhir; 7. Pernyataan Dosen Tetap (jika PT asal tutup). Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Rekomendasi Beasiswa Dosen",
    "description": "Layanan rekomendasi bagi dosen untuk melamar beasiswa (BPadden/BUDI).",
    "content_raw": "Persyaratan Pelayanan: 1. SK Dosen Tetap Yayasan; 2. Formulir Beasiswa; 3. KTP; 4. Pernyataan tidak terima beasiswa lain; 5. SK Mengajar 2 thn terakhir; 6. Perjanjian terkait sertifikasi; 7. Pernyataan bukan PNS instansi lain; 8. Surat Permohonan; 9. Bukti Registrasi Online Beasiswa; 10. Ijazah/Transkrip S1 & S2; 11. SK PNS (Dosen DPK); 12. Kontrak dengan PT Pengirim; 13. Pernyataan bersedia lapor jika lulus. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Migrasi Data PDDIKTI",
    "description": "Layanan migrasi data PDDikti akibat penggabungan atau perubahan bentuk PT.",
    "content_raw": "Persyaratan Pelayanan: 1. Scan Surat Permohonan Pimpinan PT; 2. Scan SK Penggabungan/Alih Kelola/Perubahan Nomenklatur. Prosedur: Login pddikti-admin, ajukan menu kelembagaan, upload syarat, verifikasi JFU, proses lanjut di Pusat. Jangka Waktu: 10 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Pendataan Mahasiswa Lampau",
    "description": "Layanan pembukaan periode pelaporan untuk data mahasiswa lampau.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat permohonan Pimpinan PT (Jenjang, Prodi, Semester, Alasan); 2. SPTJM Pimpinan PT bermaterai dengan daftar mahasiswa; 3. Surat hasil verifikasi pendataan mahasiswa lampau LLDIKTI IX. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Perbaikan Laporan PDDIKTI Tipe 1",
    "description": "Layanan pembukaan periode pelaporan untuk perbaikan data Tipe 1 (Data Pokok Mahasiswa).",
    "content_raw": "Persyaratan Pelayanan: 1. Surat permohonan Pimpinan PT; 2. SPTJM Pimpinan PT bermaterai; 3. Surat hasil verifikasi data tipe 1 LLDIKTI IX. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Perbaikan Laporan PDDIKTI Tipe 2",
    "description": "Layanan pembukaan periode pelaporan untuk perbaikan data Tipe 2 (Data Akademik/Nilai).",
    "content_raw": "Persyaratan Pelayanan: 1. Surat permohonan Pimpinan PT (Jenjang, Prodi, Semester, Alasan, Lampiran data). Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Perubahan Data Dosen Pada PDDIKTI",
    "description": "Layanan perubahan data pokok, fungsional, kepangkatan, pendidikan, atau sertifikasi dosen.",
    "content_raw": "Persyaratan Pelayanan: 1. Surat Pengantar PT; 2. Surat Pernyataan Pimpinan PT; 3. Dokumen pendukung sesuai data (KTP, SK Pengangkatan, SK Jafung, SK Inpassing, Ijazah, Serdik). Prosedur melalui aplikasi SISTER. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Perubahan Nomor Registrasi Dosen Pada PDDIKTI",
    "description": "Layanan perubahan tipe registrasi dosen (NIDN ke NIDK, NUP, dll).",
    "content_raw": "Persyaratan Pelayanan: Dokumen lengkap sesuai tujuan perubahan (NIDN/NIDK/NUP) meliputi KTP, SK Dosen, Ijazah, Surat Sehat/Narkoba, Surat Pernyataan Pimpinan, Perjanjian Kerja. Prosedur via pddikti-admin. Jangka Waktu: 5 hari kerja (di LLDIKTI) + 40 hari kerja (di Pusat).",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Registrasi Dosen Baru Pada PDDIKTI",
    "description": "Layanan pendaftaran nomor registrasi baru bagi dosen (NIDN, NIDK, NUP).",
    "content_raw": "Persyaratan Pelayanan: Dokumen lengkap sesuai jenis registrasi (KTP, Foto, SK Dosen, Ijazah, Surat Sehat Jasmani/Rohani/Narkoba, Perjanjian Kerja, Pernyataan Pimpinan). Untuk Dosen Asing butuh KITAS & Jabatan Assoc. Prof. Prosedur via pddikti-admin. Jangka Waktu: 5 hari kerja (di LLDIKTI) + 40 hari kerja (di Pusat).",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Pengajuan Penerbitan Akun atau Reset Password PDDIKTI",
    "description": "Layanan pembuatan akun baru atau reset password untuk operator PDDikti.",
    "content_raw": "Persyaratan Pelayanan: 1. Scan SK Operator; 2. Scan Surat Permohonan Pimpinan PT (ada email pribadi operator); 3. Pakta Integritas. Prosedur via pddikti-admin. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  },
  {
    "title": "Standar Pelayanan Publik Usulan Pindah Homebase Dosen Pada PDDIKTI",
    "description": "Layanan teknis pemindahan data homebase dosen di sistem PDDikti.",
    "content_raw": "Persyaratan Pelayanan: 1. KTP; 2. SK Pemberhentian/Lolos Butuh PT Asal; 3. Rekomendasi LLDIKTI (jika lintas wilayah); 4. SK Dosen Tetap/Kesediaan Menerima PT Tujuan; 5. Surat Pernyataan Dosen Bermaterai; 6. Rekomendasi Kepala LLDIKTI IX. Jangka Waktu: 5 hari kerja.",
    "is_active": True
  }
]

# Loop untuk mengirim data satu per satu
for item in data_list:
    try:
        response = requests.post(url, headers=headers, json=item)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Berhasil menambahkan: {item['title']}")
        else:
            print(f"Gagal ({response.status_code}): {item['title']} - {response.text}")
    except Exception as e:
        print(f"Error pada {item['title']}: {e}")