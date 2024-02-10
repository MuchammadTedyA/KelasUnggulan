from django.db import models

# Create your models here.


class siswa(models.Model):
    nisn_siswa = models.CharField(max_length=10, primary_key=True)
    nama_siswa = models.CharField(max_length=50)
    iq_siswa = models.IntegerField()
    iq_siswa_h = models.CharField(max_length=2)
    tpa_ipa_siswa = models.FloatField()
    tpa_ips_siswa = models.FloatField()
    tpa_bahasa_siswa = models.FloatField()
    tpa_ipa_siswa_h = models.CharField(max_length=3, null=True)
    tpa_ips_siswa_h = models.CharField(max_length=3, null=True)
    tpa_bahasa_siswa_h = models.CharField(max_length=3, null=True)
    rapor_ipa_siswa = models.FloatField()
    rapor_ips_siswa = models.FloatField()
    rapor_bahasa_siswa = models.FloatField()
    rapor_ipa_siswa_h = models.CharField(max_length=3, null=True)
    rapor_ips_siswa_h = models.CharField(max_length=3, null=True)
    rapor_bahasa_siswa_h = models.CharField(max_length=3, null=True)

    def __str__(self) -> str:
        return super().__str__()


class kriteria(models.Model):
    id_kriteria = models.CharField(max_length=2, primary_key=True)
    nama_kriteria = models.CharField(max_length=20)
    bobot_kriteria = models.FloatField(null=True)
    # bobot_hasil_kriteria = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__()


class sub_kriteria(models.Model):
    id_subkriteria = models.CharField(max_length=3, primary_key=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    nama_subkriteria = models.CharField(max_length=20)
    bobot_subkriteria = models.FloatField(null=True)
    # bobot_subkriteria = models.FloatField(default=0.0)
    # bobot_hasil_subkriteria = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__()


class bobot_kriteria_ahp(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    kriteria1 = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    kriteria2 = models.CharField(max_length=2, null=True)
    bobotk1 = models.FloatField()
    bobotk2 = models.FloatField(null=True)
    bobot_normal = models.FloatField(null=True)
    nilai_norm = models.FloatField(null=True)
    nilai_konsistensi = models.FloatField(null=True)
    # bobot_subkriteria = models.FloatField(default=0.0)
    # bobot_hasil_subkriteria = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__()


class bobot_subkriteria_ahp(models.Model):
    id = models.CharField(max_length=9, primary_key=True)
    subkriteria1 = models.ForeignKey(
        'sub_kriteria', on_delete=models.CASCADE, null=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    subkriteria2 = models.CharField(max_length=3, null=True)
    bobotk1 = models.FloatField()
    bobotk2 = models.FloatField(null=True)
    bobot_normal = models.FloatField(null=True)
    nilai_norm = models.FloatField(null=True)
    nilai_konsistensi = models.FloatField(null=True)
    # bobot_subkriteria = models.FloatField(default=0.0)
    # bobot_hasil_subkriteria = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__()


class sum_kriteria_ahp(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    sum_ahp = models.FloatField()
    bobot_ahp = models.FloatField(null=True)
    sum_kosistensi = models.FloatField(null=True)
    sum_kosistensi2 = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()


class sum_subkriteria_ahp(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    subkriteria = models.ForeignKey(
        'sub_kriteria', on_delete=models.CASCADE, null=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    sum_ahp = models.FloatField()
    bobot_ahp = models.FloatField(null=True)
    sum_kosistensi = models.FloatField(null=True)
    sum_kosistensi2 = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()


class skala_fuzzy(models.Model):
    id = models.CharField(max_length=1, primary_key=True)
    l = models.FloatField()
    m = models.FloatField(null=True)
    u = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()


class skala_fuzzy2(models.Model):
    id = models.CharField(max_length=1, primary_key=True)
    l = models.FloatField()
    m = models.FloatField(null=True)
    u = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()


class bobot_kriteria_fahp(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    kriteria1 = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    kriteria2 = models.CharField(max_length=2, null=True)
    bobotk1 = models.ForeignKey(
        'skala_fuzzy', on_delete=models.CASCADE, null=True)
    bobotk2 = models.ForeignKey(
        'skala_fuzzy2', on_delete=models.CASCADE, null=True)
    # jumlah_l = models.FloatField(null=True)n
    # bobot_subkriteria = models.FloatField(default=0.0)
    # bobot_hasil_subkriteria = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__()


class bobot_subkriteria_fahp(models.Model):
    id = models.CharField(max_length=9, primary_key=True)
    subkriteria1 = models.ForeignKey(
        'sub_kriteria', on_delete=models.CASCADE, null=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    subkriteria2 = models.CharField(max_length=3, null=True)
    bobotk1 = models.ForeignKey(
        'skala_fuzzy', on_delete=models.CASCADE, null=True)
    bobotk2 = models.ForeignKey(
        'skala_fuzzy2', on_delete=models.CASCADE, null=True)
    # jumlah_l = models.FloatField(null=True)n
    # bobot_subkriteria = models.FloatField(default=0.0)
    # bobot_hasil_subkriteria = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return super().__str__()


class sum_kriteria_fahp(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    jumlah_l = models.FloatField(null=True)
    jumlah_m = models.FloatField(null=True)
    jumlah_u = models.FloatField(null=True)
    si_l = models.FloatField(null=True)
    si_m = models.FloatField(null=True)
    si_u = models.FloatField(null=True)


class sum_subkriteria_fahp(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    subkriteria = models.ForeignKey(
        'sub_kriteria', on_delete=models.CASCADE, null=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    jumlah_l = models.FloatField(null=True)
    jumlah_m = models.FloatField(null=True)
    jumlah_u = models.FloatField(null=True)
    si_l = models.FloatField(null=True)
    si_m = models.FloatField(null=True)
    si_u = models.FloatField(null=True)


class derajat_probabilitas(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    nilai = models.FloatField(null=True)
    kriteria1 = models.CharField(max_length=20, null=True)
    kriteria2 = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return super().__str__()


class derajat_probabilitas_sub(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    subkriteria = models.ForeignKey(
        'sub_kriteria', on_delete=models.CASCADE, null=True)
    kriteria = models.ForeignKey(
        'kriteria', on_delete=models.CASCADE, null=True)
    nilai = models.FloatField(null=True)
    subkriteria1 = models.CharField(max_length=20, null=True)
    subkriteria2 = models.CharField(max_length=20, null=True)

    def __str__(self) -> str:
        return super().__str__()


class hasil(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    siswa = models.ForeignKey('siswa', on_delete=models.CASCADE)
    kriteria = models.ForeignKey('kriteria', on_delete=models.CASCADE)
    subkriteria = models.ForeignKey(
        'sub_kriteria', on_delete=models.CASCADE)
    nilai_sub = models.FloatField(null=True)
    nilai_kriteria = models.FloatField(null=True)

    def __str__(self) -> str:
        return super().__str__()


class laporan_hasil(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    nama = models.CharField(max_length=50)
    tanggal = models.DateField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return super().__str__()


class laporan_hasil_d(models.Model):
    laporan_hasil = models.ForeignKey(
        'laporan_hasil', on_delete=models.CASCADE)
    siswa = models.ForeignKey('siswa', on_delete=models.CASCADE)
    # kriteria = models.ForeignKey('kriteria', on_delete=models.CASCADE)
    nilai_sub1 = models.FloatField()
    nilai_kriteria1 = models.FloatField()
    nilai_sub2 = models.FloatField()
    nilai_kriteria2 = models.FloatField()
    nilai_sub3 = models.FloatField()
    nilai_kriteria3 = models.FloatField()
    nilai_sum = models.FloatField()


class hasil_dummy(models.Model):
    id_dummy = models.AutoField(primary_key=True)
    siswa = models.ForeignKey('siswa', on_delete=models.CASCADE)
    # kriteria = models.ForeignKey('kriteria', on_delete=models.CASCADE)
    nilai_sub1 = models.FloatField()
    nilai_sub2 = models.FloatField()
    nilai_sub3 = models.FloatField()


class hasil_dummy1(models.Model):
    siswa = models.ForeignKey('siswa', on_delete=models.CASCADE)
    # kriteria = models.ForeignKey('kriteria', on_delete=models.CASCADE)
    nilai_sub1 = models.FloatField()
    nilai_sub2 = models.FloatField()
    nilai_sub3 = models.FloatField()
