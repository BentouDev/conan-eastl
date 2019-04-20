if ($env:CONAN_VISUAL_VERSIONS -eq 16)
{
    choco install visualstudio2019buildtools --package-parameters "--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --quiet --locale en-US" --confirm
}