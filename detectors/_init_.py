cat > detectors/__init__.py << 'EOF'
from detectors.wordpress_detect import WordPressDetection
from detectors.version import WordPressVersion
from detectors.theme_plugin_enum import ThemePluginEnum
from detectors.exposed_endpoints import ExposedEndpoints
from detectors.directory_listing import DirectoryListing
from detectors.debug_exposure import DebugExposure
from detectors.backdoor_patterns import BackdoorPatterns
from detectors.security_headers import SecurityHeaders
from detectors.authentication import Authentication
from detectors.misconfig import Misconfig
from detectors.sensitive_files import SensitiveFiles

detector_classes = [
    WordPressDetection,
    WordPressVersion,
    ThemePluginEnum,
    ExposedEndpoints,
    DirectoryListing,
    DebugExposure,
    BackdoorPatterns,
    SecurityHeaders,
    Authentication,
    Misconfig,
    SensitiveFiles
]
EOF